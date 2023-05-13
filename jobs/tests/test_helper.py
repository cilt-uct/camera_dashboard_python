venues = ["venue1", "-venue2", "venue3%", "*venue*"]

items_rtsp = [
    {
        "key": "capture.device.presenter.src",
        "value": "rtsp://test.uct/test"
    }
]

items_rtspt = [
    {
        "key": "capture.device.presenter.src",
        "value": "rtspt://test.uct/test"
    }
]

items_no_url = [
    {
        "key": "capture.device.presenter.src",
        "value": "test"
    }
]

venue_with_items = {
    "name": "hahn",
    "state": "offline",
    "url": "100.100.100.100",
    "time-since-last-update": 28017980605,
    "capabilities": {
        "item": [
            {
                "key": "capture.device.presenter.outputfile",
                "value": "presenter.mkv"
            }, {
                "key": "capture.device.presenter.src",
                "value": "rtsp://hahn.com/axis-media/media.amp"
            }
        ]
    }
}

venue_with_single_item = {
    "name": "hani",
    "state": "idle",
    "url": "100.100.100.100",
    "time-since-last-update": 8773,
    "capabilities": {
        "item": {
            "key": "capture.device.names",
            "value": "defaults"
        }
    }
}
