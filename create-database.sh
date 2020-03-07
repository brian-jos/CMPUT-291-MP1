#!/bin/bash
sqlite3 mp1-database.db < mp1-tables.sql && sqlite3 mp1-database.db < mp1-data.sql
