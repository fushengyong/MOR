#!/usr/bin/env python2
import os
import sys
import logging
import warnings
import argparse
import numpy as np
import tensorflow as tf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from shutil import copyfile, rmtree
from datetime import datetime
from cfg.config import Config
from algorithms.NES import NES
from algorithms.ES import ES
from algorithms.entropy_ES import EntES
from algorithms.CMA_ES import CMA_ES
import matplotlib.pyplot as plt

def config(log_file):
	logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(message)s')
	warnings.simplefilter('ignore', np.RankWarning)

def set_seeds(seed):
	np.random.seed(0)
	tf.set_random_seed(0)

def get_args():
	parser = argparse.ArgumentParser(description="Flags to toggle options")
	parser.add_argument('config', nargs='?', default="cfg/Config.yaml", help='Config file specified from the cfg/ directory. Usage: `python train.py <FILENAME>.yaml`')
	parser.add_argument('-d', action='store_true', default=False, help='Debug flag, Delete log after training is finished.')
	return parser.parse_args()

def create_training_contents():
	timestamp = datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
	try:
		os.makedirs("ext/" + timestamp)
	except OSError as e:
		if e.errno != errno.EEXIST: raise
	training_directory = "ext/" + timestamp + "/"
	log_file = training_directory + timestamp + '.log'
	return training_directory, log_file, timestamp

def get_config_file():
	if not args.config:
		raise Exception("Config file not specified. Please specify a file from the cfg/ directory. Usage: `python train.py <FILENAME>.yaml`")
	config_path = "cfg/" + sys.argv[1]
	if not os.path.exists(config_path):
		raise Exception("Config file not found in cfg/ directory. Usage: `python train.py <FILENAME>.yaml`")
	return config_path

if __name__ == "__main__":

	args = get_args()
	training_directory, log_file, timestamp = create_training_contents()
	config(log_file)
	config_path = get_config_file()
	copyfile(config_path, training_directory + timestamp + ".yaml")

	try:
		set_seeds(0)
		config = Config(config_path).config
		algorithms = {"CMA_ES": CMA_ES, "ES": ES, "NES": NES, "EntES": EntES}
		algorithm = algorithms[config['algorithm']](training_directory, config)
		print("Running %s Algorithm..." % (config['algorithm']))
		print("Check {} for progress".format(log_file))
		algorithm.run()
		# set_seeds(0)
		# config = Config(config_path).config
		# algorithms = {"CMA_ES": CMA_ES, "ES": ES, "NES": NES, "EntES": EntES}
		# algorithm = algorithms[config['algorithm']](training_directory, config)
		# print("Running %s Algorithm..." % (config['algorithm']))
		# print("Check {} for progress".format(log_file))
		# cma_master, cma_popl = CMA_ES(training_directory, config).run()
		# es_master, es_popl = ES(training_directory, config).run()
		# plt.title("CMA-ES vs ES: Master Rewards")
		# plt.plot(range(len(cma_master)), cma_master, color="red", label="CMA-ES")
		# plt.plot(range(len(es_master)), es_master, color="green", label="ES")
		# plt.legend()
		# plt.savefig(training_directory + "test-master.png")
		# plt.clf()
		# plt.title("CMA-ES vs ES: Population Rewards")
		# plt.plot(range(len(cma_popl)), cma_popl, color="red", label="CMA-ES")
		# plt.plot(range(len(es_popl)), es_popl, color="green", label="ES")
		# plt.legend()
		# plt.savefig(training_directory + "test-population.png")
		# plt.clf()
	except KeyboardInterrupt:
		if args.d:
			print("\nDeleted: {}".format(training_directory))
			rmtree(training_directory)
		sys.exit(1)

	if args.d:
		print("\nDeleted Training Folder: {}".format(training_directory))
		rmtree(training_directory)
