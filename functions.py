# coding='utf-8'
functions = [
    {
        "name": "img_generation",
        "description": "Generate an image based on the text description of the image",
        "parameters": {
            "type": "object",
            "properties": {
                "image_description": {
                    "type": "string",
                    "description": "The text used to describe the image to be generated should include details about "
                                   "the background and the object",
                },
                "image_num": {
                    "type": "string",
                    "description": "The number of images generated",
                },
            },
            "required": ["image_description", "image_num", "size"],
        }
    },
    {
        "name": "get_weather_info",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Chinese place names ending in 'city', 'county', 'district' and 'banner'"
                },
            },
            "required": ["location"],
        }
    }
]
