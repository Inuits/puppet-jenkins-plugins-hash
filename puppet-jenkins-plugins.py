#!/usr/bin/env python
import logging
import os
import yaml
import json
import requests
import argparse

class PuppetJenkinsPlugins:
    def __init__(self):
        pass

    def parse_options(self):
        parser = argparse.ArgumentParser(prog='puppet-jenkins-plugins',
                                         description='''
                                         Takes a yaml file as input containing plugins that can be
                                         used as jenkins::plugins_hash puppet parameters, and add
                                         missing dependencies to the list.
                                         ''')
        parser.add_argument('yaml', help='configuration file to use')
        parser.add_argument('--update-center-json', help='Update center JSON url',
                            default='https://updates.jenkins-ci.org/current/update-center.json')
        parser.add_argument('--debug', '-d', help='Print debug information', action='store_true')
        args = parser.parse_args()
        if args.debug:
            logging.basicConfig(level=logging.DEBUG)
        logging.debug('Parsing options...')
        self.input_yaml = args.yaml
        logging.debug('Yaml file is %s' % self.input_yaml)
        self.update_center_json = args.update_center_json
        logging.debug('update_center_json is %s' % self.update_center_json)

    def run(self):
        self.parse_options()
        self.fetch_update_center_json()
        self.parse_dependencies()

    def parse_plugin_dependencies(self, name, config):
        deps = {}
        if not name in self.plugins_data:
            raise Exception('No plugin %s' % name)
        plugin_data = self.plugins_data[name]
        if 'dependencies' in plugin_data:
            for dep in plugin_data['dependencies']:
                if dep['name'] == 'credentials':
                    continue
                if dep['optional'] == False:
                    deps[dep['name']] = dep['version']
                for dep, values in list(deps.items()):
                    deps.update(self.parse_plugin_dependencies(dep, values))


        deps[name] = {'version': plugin_data['version']}
        return deps

    def parse_dependencies(self):
        output_data = {}
        with open(self.input_yaml) as input_yaml:
            input_data = yaml.load(input_yaml)
        for plugin in input_data:
            dependencies = self.parse_plugin_dependencies(plugin, input_data)
            for dep, keys in dependencies.items():
                output_data[dep] = keys

        print(yaml.safe_dump(output_data))

    def fetch_update_center_json(self):
        if os.path.isfile(self.update_center_json):
            with open(self.update_center_json) as f:
                self.plugins_data = json.loads(f.readlines()[1])['plugins']
            return
        logging.debug('Fetching JSON')
        response = requests.get(self.update_center_json)
        self.plugins_data = json.loads(response.text.split('\n')[1])['plugins']

if __name__ == '__main__':
    PuppetJenkinsPlugins().run()

