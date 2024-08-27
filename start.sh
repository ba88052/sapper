#!/bin/bash
gunicorn --timeout 0 main:app
