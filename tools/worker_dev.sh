#!/bin/bash

../bin/celery worker --app=app.tasks -l info
