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
![image](https://user-images.githubusercontent.com/3003773/197098406-c7160300-b1a9-46e2-b00e-198b7f95003f.png)

## *Notice: This is a work in progress, all help is welcome :)*


