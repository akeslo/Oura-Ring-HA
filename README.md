## *Notice: This is a work in progress, all help is welcome :)*

# Oura Ring HA

# Summary
A custom component to display the [Oura Ring](https://cloud.ouraring.com/docs/) data from the [v2 API](https://cloud.ouraring.com/docs/)

# Installation
This can be installed via HACS or by copying all the files from custom_components/oura_ring_ha/ to <config directory>/custom_components/oura_ring_ha/.

# Configuration
Add the following to *configuration.yaml*

    # Example configuration.yaml entry
    oura_ring_ha:
    api_token: "API TOKEN HERE"

The above configuration will generate an entity with the id sensor.oura_ring_ha and current value as the sleep score along with these attributes from yesterday:

    date
    bedtime_start_hour
    bedtime_end_hour
    breath_average
    temperature_delta
    resting_heart_rate
    heart_rate_average
    deep_sleep_duration
    rem_sleep_duration
    light_sleep_duration
    total_sleep_duration
    awake_duration
    in_bed_duration

The motivation for this came from using the [oura-custom-component](https://github.com/nitobuendia/oura-custom-component) integration.

## *Notice: This is a work in progress, all help is welcome :)*

