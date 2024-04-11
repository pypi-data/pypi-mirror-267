# Dataiku CLI Requests

A small Python script to call builds for Dataiku datasets via the command line interface. 
* You can generate crons with dataiku-cli-requests command to schedule your builds!!!
* At the moment it only works with NON RECURSIVE FORCED BUILD.


## Requirements

* Python3 [https://www.python.org/]

## Installation

`pip install dataiku-cli-requests`

## Getting started

* Command arguments:
- host
- user
- password
- project
- dataset

## Example
`dataiku-cli-requests --host https://dataiku.example.com:11000/ --user test --password p4$$w0rd --project PROJECTNAME --dataset mydataset`
