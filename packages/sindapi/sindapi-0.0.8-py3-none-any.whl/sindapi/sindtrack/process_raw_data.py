import numpy as np
import re
import pickle
import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from typing import List, Dict


from ..sindmap.map_api import SinDDynamicMap
from ..sindmap.traffic_light.traffic_light import TrafficLight, LightState, SignalType
from .data_schema import Track, SinDScenario
from .utils.constants import *
from .data_schema import *



def process_raw_data(raw_data_path: Path, processed_data_path: Path) -> None:
    if not processed_data_path.exists():
        processed_data_path.mkdir(parents=True, exist_ok=True)

    for entry in raw_data_path.iterdir():
        # 检查条目是否是文件夹
        if entry.is_dir():
            record_id = entry.name
            record_path = raw_data_path.joinpath(record_id)
            print(f"Start processing record: {record_id}")
            process_one_record(record_path, processed_data_path)



def process_one_record(record_path: Path, processed_data_path: Path) -> None:
    record_steps_num = _get_record_steps_num(record_path)
    scenario_id = 1

    # 使用tqdm包装循环以监视进度
    with tqdm(total=(record_steps_num // SIND_SCENARIO_GENERATION_STEP), desc="Processing scenarios") as pbar:
        for start_frame in range(0, record_steps_num, SIND_SCENARIO_GENERATION_STEP):
            # ensure scenario length >= TOTAL_TIMESTEPS
            if record_steps_num - start_frame < SIND_SCENARIO_TOTAL_TIMESTEPS:
                break
            sind_scenario = process_one_scenario(start_frame, scenario_id, record_path)

            file_name = f"{sind_scenario.record_id}_{sind_scenario.scenario_id}.pkl"
            save_path = processed_data_path / file_name
            with open(save_path, 'wb') as file:
                pickle.dump(sind_scenario, file)

            scenario_id += 1
            pbar.update(1)  # 更新进度条




def _get_record_steps_num(record_path: Path) -> int:
    df = pd.read_csv(record_path / 'Veh_tracks_meta.csv')
    max_final_frame = df['finalFrame'].max()

    # record_id = record_path.stem
    # record_id = re.sub(r'(\d)_(\d{1})(_\d)', r'\1_0\2\3', record_id)
    # df_traffic_light = pd.read_csv(record_path / f'TrafficLight_{record_id}.csv')
    # max_traffic_light_time_stamp_ms = df_traffic_light['timestamp(ms)'].max()
    #
    # # the traffic light state should include all track info
    # if _get_time_stamp_ms_from_frame(max_final_frame) >= max_traffic_light_time_stamp_ms:
    #     print(f"{record_id} tl need to be checked")

    return max_final_frame


def _get_time_stamp_ms_from_frame(frame_id: int) -> float:
    return frame_id * (3 * 1000 / SIND_SCENARIO_RECORD_STEP_HZ)

def process_one_scenario(start_frame: int, scenario_id: int, record_path: Path) -> SinDScenario:
    record_id = record_path.stem
    city_name = record_path.parts[-3]
    frame_ids = list(range(start_frame, start_frame + SIND_SCENARIO_TOTAL_TIMESTEPS))
    end_frame = frame_ids[-1]
    timestamps_ms = [_get_time_stamp_ms_from_frame(frame_id) for frame_id in frame_ids]

    tracks = get_tracks(record_path, start_frame, end_frame)

    focal_track_id = None
    for track in tracks.values():
        if track.category.value >= TrackCategory.SCORED_TRACK.value and track.object_type == ObjectType.CAR:
            focal_track_id = track.track_id
            break

    # TODO: need to debug at line 228
    dynamic_map = get_dynamic_map(record_path, timestamps_ms)

    sind_scenario = SinDScenario(
        scenario_id=scenario_id,
        record_id=record_id,
        timestamps_ms=timestamps_ms,
        tracks=tracks,
        focal_track_id=focal_track_id,
        city_name=city_name,
        # dynamic_map=dynamic_map,
        # map_id=dynamic_map.map_id
    )

    return sind_scenario

def get_tracks(record_path: Path, start_frame: int, end_frame: int) -> Dict[str, Track]:
    df_vehicle_meta = pd.read_csv(record_path / 'Veh_tracks_meta.csv')
    df_vehicle_meta = df_vehicle_meta[
        ((start_frame <= df_vehicle_meta['initialFrame']) & (df_vehicle_meta['initialFrame'] <= end_frame))
        | ((start_frame <= df_vehicle_meta['finalFrame']) & (df_vehicle_meta['finalFrame'] <= end_frame))]

    attribute_dict = {}
    for index, row in df_vehicle_meta.iterrows():
        track_id = str(row['trackId'])
        width = row['width']
        length = row['length']
        class_ = row['class']
        cross_type = row['CrossType']
        signal_violation_behavior = row['Signal_Violation_Behavior']

        attribute_dict[track_id] = {
            'width': width,
            'length': length,
            'class': class_,
            'CrossType': cross_type,
            'Signal_Violation_Behavior': signal_violation_behavior
        }

    df_vehicle_track = pd.read_csv(record_path / 'Veh_smoothed_tracks.csv')
    states_dict = {}
    for track_id in attribute_dict.keys():
        # 根据 trackId 在 DataFrame 中选择相应的行
        track_df = df_vehicle_track[(df_vehicle_track['track_id'].astype(str)) == track_id]

        # 根据 start frame 和 end frame 在指定范围内选择行
        selected_df = track_df[(track_df['frame_id'] >= start_frame) & (track_df['frame_id'] <= end_frame)]

        # 生成 observed 列表
        observed = [0] * (end_frame - start_frame + 1)
        for frame_id in selected_df['frame_id'].tolist():
            observed[frame_id - start_frame] = 1

        # 选择满足条件的 x, y, vx, vy, yaw_rad 列，并生成对应的值列表
        x_values = [0] * (end_frame - start_frame + 1)
        y_values = [0] * (end_frame - start_frame + 1)
        vx_values = [0] * (end_frame - start_frame + 1)
        vy_values = [0] * (end_frame - start_frame + 1)
        heading_rad_values = [0] * (end_frame - start_frame + 1)
        for index, row in selected_df.iterrows():
            frame_id = row['frame_id']
            x_values[frame_id - start_frame] = row['x']
            y_values[frame_id - start_frame] = row['y']
            vx_values[frame_id - start_frame] = row['vx']
            vy_values[frame_id - start_frame] = row['vy']
            heading_rad_values[frame_id - start_frame] = row['yaw_rad']

        # 将结果存储到字典中
        states_dict[track_id] = {
            'x': x_values,
            'y': y_values,
            'vx': vx_values,
            'vy': vy_values,
            'yaw_rad': heading_rad_values,
            'observed': observed
        }

    track_dict = {
        track_id: {**attribute_dict[track_id], 'states': states_dict[track_id]}
        for track_id in attribute_dict
    }

    tracks = {}
    for track_id, track_info in track_dict.items():
        object_type = ObjectType(track_info['class'])
        object_attribute = ObjectAttribute(
            length=track_info['length'],
            width=track_info['width'],
            crosstype=CrossType(track_info['CrossType']),
            violation=ViolationType(track_info['Signal_Violation_Behavior'])
        )

        state = track_info['states']
        object_states = []
        for timestep in range(SIND_SCENARIO_TOTAL_TIMESTEPS):
            object_state = ObjectState(
                observed=bool(state['observed'][timestep]),
                timestep=timestep,
                position=(state['x'][timestep],state['y'][timestep]),
                heading=state['yaw_rad'][timestep],
                velocity=(state['vx'][timestep],state['vy'][timestep]),
            )
            object_states.append(object_state)

        if sum(state['observed'][:SIND_SCENARIO_OBS_TIMESTEPS]) < SIND_SCENARIO_OBS_TIMESTEPS // 2:
            category = TrackCategory.TRACK_FRAGMENT
        elif sum(state['observed'][SIND_SCENARIO_OBS_TIMESTEPS:]) < SIND_SCENARIO_PRED_TIMESTEPS:
            category = TrackCategory.UNSCORED_TRACK
        elif sum(state['observed'][:SIND_SCENARIO_OBS_TIMESTEPS]) < SIND_SCENARIO_OBS_TIMESTEPS:
            category = TrackCategory.SCORED_TRACK
        else:
            category = TrackCategory.FOCAL_TRACK

        track = Track(
            track_id=track_id,
            object_states=object_states,
            object_type=object_type,
            category=category,
            object_attribute=object_attribute
        )
        tracks[track_id] = track



    return tracks

def get_dynamic_map(record_path: Path, timestamps_ms: List[float]):
    record_id = record_path.stem
    record_id = re.sub(r'(\d)_(\d{1})(_\d)', r'\1_0\2\3', record_id)
    df_traffic_light = pd.read_csv(record_path / f'TrafficLight_{record_id}.csv')

    tl1_states = []
    tl2_states = []
    for idx, timestamp in enumerate(timestamps_ms):
        closest_row = df_traffic_light[df_traffic_light['timestamp(ms)'] <= timestamp].iloc[-1]
        closest_row_index = df_traffic_light.index.get_loc(closest_row.name)

        if closest_row_index >= len(df_traffic_light) - 1:
            # TODO: 8_10_1, 8_03_1, 8_03_2, 8_05_3, 8_06_3, 8_09_3, 8_09_4, need to be add TL data
            # if closest_row is the last row
            remaining_second1 = None
            remaining_second2 = None
            tl1_signal = SignalType.UNKNOWN
            tl2_signal = SignalType.UNKNOWN
            return
        else:
            tl1_signal = closest_row['Traffic light 1']
            tl2_signal = closest_row['Traffic light 2']



            next_tl1_row = df_traffic_light.iloc[closest_row_index + 1:]
            desired_row_tl1 = next_tl1_row[next_tl1_row['Traffic light 1'] != tl1_signal]
            if not desired_row_tl1.empty:
                desired_row_tl1 = desired_row_tl1.iloc[0]
                remaining_second1 = desired_row_tl1['timestamp(ms)'] - timestamp

            else:
                # TODO: 检索不到下一行状态变化，统计红绿灯时间
                last_row = df_traffic_light.iloc[-1]
                remaining_second1 = last_row['timestamp(ms)'] - timestamp
                assert remaining_second1 > 0

            next_tl2_row = df_traffic_light.iloc[closest_row_index + 1:]
            desired_row_tl2 = next_tl2_row[next_tl2_row['Traffic light 2'] != tl2_signal]
            if not desired_row_tl2.empty:
                desired_row_tl2 = desired_row_tl2.iloc[0]
                remaining_second2 = desired_row_tl2['timestamp(ms)'] - timestamp

            else:
                last_row = df_traffic_light.iloc[-1]
                remaining_second2 = last_row['timestamp(ms)'] - timestamp
                assert remaining_second2 > 0

            remaining_second1 = int(remaining_second1 / 1000)
            remaining_second2 = int(remaining_second2 / 1000)

        tl1_state = LightState(idx, SignalType.from_int(int(tl1_signal)), remaining_second1)
        tl2_state = LightState(idx, SignalType.from_int(int(tl2_signal)), remaining_second2)
        tl1_states.append(tl1_state)
        tl2_states.append(tl2_state)

    dynamic_map_path = record_path.parents[1] / 'map/dynamic_map.json'
    with open(dynamic_map_path, 'r') as file:
        dynamic_map_data = json.load(file)

    traffic_lights = {}
    for tl in dynamic_map_data['traffic_light']:
        if tl['id'] == 1:
            tl1 = TrafficLight(
                id=1,
                controlled_stretches=tl['controlled_stretches'],
                controlled_intersections=tl['controlled_intersections'],
                light_states=tl1_states
            )
            traffic_lights[1] = tl1
        if tl['id'] == 2:
            tl2 = TrafficLight(
                id=2,
                controlled_stretches=tl['controlled_stretches'],
                controlled_intersections=tl['controlled_intersections'],
                light_states=tl2_states
            )
            traffic_lights[2] = tl2

    return SinDDynamicMap(
        city_name=dynamic_map_data['city_name'],
        traffic_lights=traffic_lights,
        map_id=dynamic_map_data['map_id']
    )
