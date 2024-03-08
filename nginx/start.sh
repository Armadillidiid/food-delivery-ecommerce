#!/bin/bash

# Reload nginx every 6 hours
'/bin/sh -c ''while :; do sleep 6h & wait $${!}; nginx -s reload; done;"'''
