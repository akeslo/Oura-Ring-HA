## *Notice: This is a work in progress, all help is welcome :)*

# Oura Ring Sensors

# Summary
A custom component to display the [Oura Ring](https://cloud.ouraring.com/) data from the [v2 API](https://cloud.ouraring.com/docs/)

# Installation
This can be installed via HACS or by copying all the files from custom_components/oura_ring_ha/ to <config directory>/custom_components/ouraring/.

# Configuration
Add the following to *configuration.yaml*

    # Example configuration.yaml entry
    sensor:
    
        - platform: ouraring
          api_token: API_TOKEN_HERE

The above configuration will generate the following sensor entities with the state set as the Oura score for each category respectively
   
   - oura_ring_sleep
   ![image](https://user-images.githubusercontent.com/3003773/197370662-e41a9230-ad9d-4196-81d8-7e2a918dacbd.png)

   - oura_ring_activity
   ![image](https://user-images.githubusercontent.com/3003773/197370672-82df839d-fbcc-4461-ae85-9314d33cea5f.png)

   - oura_ring_readiness
    
The motivation for this came from using the [oura-custom-component](https://github.com/nitobuendia/oura-custom-component) integration.

## Example
![image](https://user-images.githubusercontent.com/3003773/200173350-56aa00d8-b9d6-4e54-a060-eb74ea6be13d.png)
![image](https://user-images.githubusercontent.com/3003773/200173295-42f1170b-71af-40bf-a16b-28aa923485ac.png)
![image](https://user-images.githubusercontent.com/3003773/200173308-ffb83d9b-01da-41c6-a638-b830ec721730.png)
![image](https://user-images.githubusercontent.com/3003773/200173336-5dcefe12-6777-4ae7-9307-8abef817dd6b.png)

```
type: vertical-stack
cards:
  - type: entities
    title: Wellness Indicators
    entities:
      - entity: sensor.bed_time_yesterday
        name: Bed Time
      - entity: sensor.wake_time_yesterday
        name: Wake Time
        secondary_info: none
      - type: custom:template-entity-row
        name: Calories Burned
        state: >-
          {{ "{:,}
          cals".format(states.sensor.oura_ring_activity.attributes.data.total_calories)
          }}
        entity: sensor.oura_ring_activity
        icon: mdi:fire
        unit: Cals
      - type: custom:template-entity-row
        name: Active Calories Burned
        state: >-
          {{ states.sensor.oura_ring_activity.attributes.data.active_calories }}
          / {{ states.sensor.oura_ring_activity.attributes.data.target_calories
          }}
        entity: sensor.oura_ring_activity
        icon: mdi:fire-alert
      - type: custom:template-entity-row
        name: Steps
        entity: sensor.oura_ring_activity
        state: >-
          {{ "{:,}
          steps".format(states.sensor.oura_ring_activity.attributes.data.steps)
          }}
        icon: mdi:shoe-sneaker
      - type: custom:template-entity-row
        name: >-
          {{ states.sensor.oura_ring_activity.attributes.workout_1.intensity |
          capitalize }} {{
          states.sensor.oura_ring_activity.attributes.workout_1.activity |
          capitalize }} 
        entity: sensor.oura_ring_activity
        state: '{{ states.sensor.oura_ring_activity.attributes.workout_1.duration }}'
        icon: mdi:weight-lifter
        secondary: >-
          {{
          as_timestamp(states.sensor.oura_ring_activity.attributes.workout_1.date)
          | timestamp_custom("%a %b %d", True) }} 
      - type: custom:template-entity-row
        entity: sensor.oura_heart_activity
        name: Heart Activity
        secondary: >-
          {{as_timestamp(states.sensor.oura_heart_activity.attributes.state_timestamp)
          | timestamp_custom("%H:%M:%S", True) }}
  - type: custom:apexcharts-card
    apex_config:
      chart:
        height: 200px
    graph_span: 12h
    header:
      show: true
      show_states: true
      colorize_states: true
      title: Heart Rate
      standard_format: true
    series:
      - entity: sensor.oura_heart_activity
        name: Heart Rate
        data_generator: |
          return entity.attributes.timestamps.map((peak, index) => {
            return [new Date(peak).getTime(), entity.attributes.bpm[index]];
          });
        color: '#D43D54'
        stroke_width: 2
        show:
          in_header: false
  - type: custom:apexcharts-card
    apex_config:
      chart:
        height: 150px
    graph_span: 7d
    now:
      show: true
      color: red
      label: now
    header:
      show: true
      show_states: true
      colorize_states: true
      title: Oura Scores
      standard_format: true
    series:
      - entity: sensor.oura_ring_sleep
        name: Sleep
        show:
          in_chart: true
        color: '#20bf6b'
        type: column
        group_by:
          func: last
          duration: 1d
      - entity: sensor.oura_ring_readiness
        name: Readiness
        show:
          in_chart: true
        color: '#45aaf2'
        type: column
        group_by:
          func: last
          duration: 1d
      - entity: sensor.oura_ring_activity
        name: Activity
        show:
          in_chart: true
        color: '#fed330'
        type: column
        group_by:
          func: last
          duration: 1d
  - type: custom:apexcharts-card
    apex_config:
      chart:
        height: 200px
    graph_span: 7d
    header:
      show: true
      show_states: true
      colorize_states: true
      title: Sleep
      standard_format: true
    series:
      - entity: sensor.oura_ring_sleep
        name: Score
        show:
          in_chart: false
        color: white
      - entity: sensor.sleep_resting_heart_rate_yesterday
        name: HR
        show:
          in_chart: false
      - entity: sensor.time_in_bed_yesterday
        name: In Bed
        type: area
        color: grey
        group_by:
          func: last
          duration: 1d
        show:
          legend_value: false
      - entity: sensor.total_sleep_yesterday
        name: Total Sleep
        type: area
        color: purple
        group_by:
          func: last
          duration: 1d
        show:
          legend_value: false
      - entity: sensor.rem_sleep_yesterday
        name: REM
        color: '#20bf6b'
        group_by:
          func: last
          duration: 1d
        type: column
        show:
          in_header: false
      - entity: sensor.deep_sleep_yesterday
        name: Deep
        color: '#45aaf2'
        type: column
        group_by:
          func: last
          duration: 1d
        show:
          in_header: false
      - entity: sensor.light_sleep_yesterday
        name: Light
        type: column
        color: '#fed330'
        group_by:
          func: last
          duration: 1d
        show:
          in_header: false
      - entity: sensor.time_awake_yesterday
        name: Awake
        color: '#fc5c65'
        type: column
        group_by:
          func: last
          duration: 1d
        show:
          in_header: false
```

## *Notice: This is a work in progress, all help is welcome :)*


