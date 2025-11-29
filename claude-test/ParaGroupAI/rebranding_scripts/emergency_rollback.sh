#!/bin/bash

# Emergency rollback
bash rollback_all_changes.sh

# Review rollback log
cat rollback_*.log