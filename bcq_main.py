import argparse
import numpy as np
import os
import torch

import BCQ_brain
import utils

import json
from BCQ_simulation import BCQ_control
from ALINEA import coor
from generate_random_flow import random_flow
from organize_RLdata import read_detectorout
from contrast_ql_alinea import get_ttd
from nocontrol import non_control
import matplotlib.pyplot as plt

# Trains BCQ offline
def train_BCQ(state_dim, action_dim, max_action, device, args):
	# For saving files
	setting = f"{args.env}_{args.seed}"
	buffer_name = f"{args.buffer_name}_{setting}"

	# Initialize policy
	policy = BCQ_brain.BCQ(state_dim, action_dim, max_action, device, args.discount, args.tau, args.lmbda, args.phi)

	# Load buffer
	replay_buffer = utils.ReplayBuffer(state_dim, action_dim, device)
	replay_buffer.load(f"./buffers/{buffer_name}")
	
	training_iters = 0
	
	while training_iters < args.max_timesteps: 
		pol_vals = policy.train(replay_buffer, iterations=int(args.eval_freq), batch_size=args.batch_size)
		training_iters += args.eval_freq
		#eval_policy(policy, training_iters)
		print(f"Training iterations: {training_iters}")
	return policy.actor_loss, policy.critic_loss, policy.vae_loss


# Runs policy for X episodes and returns average reward
# A fixed seed is used for the eval environment
def eval_policy(BCQ, step):
    
    detector_list = ['812 SB']
    warmup = 600
    _=random_flow()
    os.system(r"duarouter -n C:\Users\Mr.Du\Desktop\30jours\RLDemo\Anet.net.xml -r C:\Users\Mr.Du\Desktop\30jours\RLDemo\random_routes.xml --randomize-flows --random -o C:\Users\Mr.Du\Desktop\30jours\RLDemo\myrandomroutes.rou.xml")
       
    non_control(0)
    ttd_non = get_ttd(0)
    _, o, _ = read_detectorout(detector_list, str(0)+'out.xml', warmup)
    o_non = o['812 SB']


    q_a, r_a, _, _ = coor(0, 18)
    ttd_a = get_ttd(18)
    _, o, _ = read_detectorout(detector_list, str(18)+'out.xml', warmup)
    o_a = o['812 SB']

    q_bcq, r_bcq, _, _ = BCQ_control(0, BCQ)
    ttd_bcq = get_ttd(0)
    _, o, _ = read_detectorout(detector_list, str(0)+'out.xml', warmup)
    o_bcq = o['812 SB']
    with open(f'oa{step}.json','w',encoding='utf-8') as f:
        json.dump(list(o_a),f,ensure_ascii=False)
    with open(f'qa{step}.json','w',encoding='utf-8') as f:
        json.dump(q_a,f,ensure_ascii=False)
    with open(f'ra{step}.json','w',encoding='utf-8') as f:
        json.dump(r_a,f,ensure_ascii=False)
    with open(f'ttda{step}.json','w',encoding='utf-8') as f:
        json.dump(ttd_a,f,ensure_ascii=False)
    with open(f'./bcqLearn/obcq{step}.json','w',encoding='utf-8') as f:
        json.dump(list(o_bcq),f,ensure_ascii=False)
    with open(f'./bcqLearn/qbcq{step}.json','w',encoding='utf-8') as f:
        json.dump(q_bcq,f,ensure_ascii=False)
    with open(f'./bcqLearn/rbcq{step}.json','w',encoding='utf-8') as f:
        json.dump(list(r_bcq),f,ensure_ascii=False)
    with open(f'./bcqLearn/ttdbcq{step}.json','w',encoding='utf-8') as f:
        json.dump(ttd_bcq,f,ensure_ascii=False)
    '''x = np.linspace(1, len(r_bcq), len(r_bcq))
    plt.plot(x, r_a)
    plt.show()
    plt.plot(x, r_bcq)
    plt.show()'''
    print("---------------------------------------")
    print(f"Evaluation over {step} steps: ALINEA:{ttd_a['mflow']:.3f}, {ttd_a['rflow']:.3f}; BCQ:{ttd_bcq['mflow']:.3f}, {ttd_bcq['rflow']:.3f}; zero:{ttd_non['mflow']:.3f}, {ttd_non['rflow']:.3f}")
    print(f"Average Occupancy: ALINEA: {np.mean(o_a):.3f}; BCQ:{np.mean(o_bcq):.3f}")
    print("---------------------------------------")
    print("---------------------------------------")
    '''print(f"Evaluation over {step} steps: BCQ:{ttd_bcq['mflow']:.3f}, {ttd_bcq['rflow']:.3f}")
    print(f"Average Occupancy:BCQ:{np.mean(o_bcq):.3f}")
    print("---------------------------------------")'''

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser()
	parser.add_argument("--env", default="Ramp")               # OpenAI gym environment name
	parser.add_argument("--seed", default=0, type=int)              # Sets Gym, PyTorch and Numpy seeds
	parser.add_argument("--buffer_name", default="Robust")          # Prepends name to filename
	parser.add_argument("--eval_freq", default=5, type=float)     # How often (time steps) we evaluate
	parser.add_argument("--max_timesteps", default=1000, type=int)   # Max time steps to run environment or train for (this defines buffer size)
	parser.add_argument("--start_timesteps", default=25e3, type=int)# Time steps initial random policy is used before training behavioral
	parser.add_argument("--rand_action_p", default=0.3, type=float) # Probability of selecting random action during batch generation
	parser.add_argument("--gaussian_std", default=0.3, type=float)  # Std of Gaussian exploration noise (Set to 0.1 if DDPG trains poorly)
	parser.add_argument("--batch_size", default=64, type=int)       # Mini batch size for networks
	parser.add_argument("--discount", default=0.9)                  # Discount factor
	parser.add_argument("--tau", default=0.005)                     # Target network update rate
	parser.add_argument("--lmbda", default=0.75)                    # Weighting for clipped double Q-learning in BCQ
	parser.add_argument("--phi", default=0.0)                      # Max perturbation hyper-parameter for BCQ
	parser.add_argument("--train_behavioral", action="store_true")  # If true, train behavioral (DDPG)
	parser.add_argument("--generate_buffer", action="store_true")   # If true, generate buffer
	args = parser.parse_args()

	print("---------------------------------------")	
	if args.train_behavioral:
		print(f"Setting: Training behavioral, Env: {args.env}, Seed: {args.seed}")
	elif args.generate_buffer:
		print(f"Setting: Generating buffer, Env: {args.env}, Seed: {args.seed}")
	else:
		print(f"Setting: Training BCQ, Env: {args.env}, Seed: {args.seed}")
	print("---------------------------------------")

	if args.train_behavioral and args.generate_buffer:
		print("Train_behavioral and generate_buffer cannot both be true.")
		exit()

	if not os.path.exists("./results"):
		os.makedirs("./results")

	if not os.path.exists("./models"):
		os.makedirs("./models")

	if not os.path.exists("./buffers"):
		os.makedirs("./buffers")
	
	state_dim = 3
	action_dim = 1
	max_action = float(8)

	device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

	#a, c, v = train_BCQ(state_dim, action_dim, max_action, device, args)
