from bitcoin import *
import sys
import qrcode
import qrcode.image.svg
from PIL import Image
import serial
import requests
def main():
	player1 = mainMenu()
	print("please send your reward of ", player1.wager, " to this address")
	player1.hardwareSig()
	player1.userAccount()
	method = 'basic'
	filename = "addyImage.PNG"

	img = qrcode.make(player1.address)
	imgFile = open(filename,'w+')
	img.save(filename,'PNG') 
	imgFile.close()
	im = Image.open('addyImage.png')
	im.show()
	datafy(player1)


def datafy(player1):
	repCounter = 0
	arduino = serial.Serial('/dev/cu.usbmodem1421', 9600, timeout=.5)
	repLevel = 4.8
	data = 0
	while repCounter <= player1.goal:
		data = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
		if data:

			print(repCounter)
			if data >= repLevel:
				repCounter += 1
				#hold(arduino, data)
			if repCounter == player1.goal:
				player1.Winning()
def hold(arduino, data):
	while data > 1:
		data = arduino.readline()[:-2] #the last bit gets rid of the new-line chars
		
			#print(data)


	#print(player1.activity, player1.wager, player1.goal)
	# if(verify_tx_input(txDone, 0, lockingScript, keys, pubkeys)):
	
	# 	print("user key signed nicely")
	# else: 
	# 	print("user key failed")
	# if(worked1 == True):
	
	# 	print("user key signed nicely")
	# else:
	# 	print("hardware key failed")
class Player:
	def setActivity(self, Activity):
		self.activity = Activity

	def setGoal(self, goal):
		self.goal = int(goal)

	def setWager(self, wager):
		self.wager = int(wager)

	def hardwareSig(self):
		self.hardwareKey = '2a32ef29d4d7dfbc150363d379b4294ed5b1eb10ce30ee74af14406ea911ea29'
		self.hardwarePubkey = privkey_to_pubkey(self.hardwareKey)

	def Winning(self):
		signedmulti2 = multisign(self.tx, 0, self.lockingScript, self.hardwareKey)
		#print("signed\n", signedmulti2)
		
		#print(signedmulti1)
		# rawVer = ecdsa_raw_verify(bin_txhash(tx, SIGHASH_ALL), der_decode_sig(signedmulti1), userPubkey)
		# if(rawVer):
		# 	print("nice")
		# worked1 = verify_tx_input(tx2, 0, lockingScript, signedmulti1, userPubkey)
		# worked2 = verify_tx_input(tx, 0, lockingScript, signedmulti2, hardwarePubkey)
		keys = [self.signedmulti1, signedmulti2]
		txDone = apply_multisignatures(self.tx, 0, self.lockingScript, keys)
		print("Congrats On Hitting Your Goal")

	def userAccount(self):
		self.userKey = '612477b03a3c06a3eed7feb2e94f0611ce7a246b192fda760ce642d57f58c59b'
		#hardwareKey = '2a32ef29d4d7dfbc150363d379b4294ed5b1eb10ce30ee74af14406ea911ea29'
		self.userPubkey = privkey_to_pubkey(self.userKey)
		#hardwarePubkey = privkey_to_pubkey(hardwareKey)
		userAddy = pubtoaddr(self.userPubkey)
		pubkeys = [self.userPubkey, self.hardwarePubkey]
		self.lockingScript = mk_multisig_script(pubkeys, 1, 2)
		# print(get_privkey_format(userKey))
		decodedPriv = decode(self.hardwareKey, 16)
		# print('privdecode \n')
		# print(decodedPriv)
		# if(is_privkey(userKey)):
		# 	print("yes priv")
		##redeem script??
		self.address = scriptaddr(self.lockingScript)
		# print("\n"+lockingScript+"\n")
		# print(self.address)
		h = history(self.address)
		r = requests.get('https://blockchain.info/rawaddr/'+self.address)
		#self.returnAddy = r.json()["txs"][0]["inputs"][0]["prev_out"]["addr"]#["txs"][0]["inputs"][0]["addr"])
		#self.userReturnAddy = 

		outs = [{'value': self.wager, 'address': '1MkJCo1RWCdndkMc5xq8s55CjhB8aZAhtK'}]
		self.tx = mktx(h, outs)
		msg = signature_form(self.tx, 0, self.lockingScript, SIGHASH_ALL)
		msgInt = int(msg, 16)
		
		#print("\nmsg", msgInt, "\n")
		msgSize = sys.getsizeof(msgInt)
		#print("\n", msgSize, "size\n")
		self.signedmulti1 = multisign(self.tx, 0, self.lockingScript, self.userKey)
		#### This needs to be done on the arduino ###
		# signedmulti2 = multisign(tx, 0, self.lockingScript, self.hardwareKey)
		# #print("signed\n", signedmulti2)
		
		# #print(signedmulti1)
		# # rawVer = ecdsa_raw_verify(bin_txhash(tx, SIGHASH_ALL), der_decode_sig(signedmulti1), userPubkey)
		# # if(rawVer):
		# # 	print("nice")
		# # worked1 = verify_tx_input(tx2, 0, lockingScript, signedmulti1, userPubkey)
		# # worked2 = verify_tx_input(tx, 0, lockingScript, signedmulti2, hardwarePubkey)
		# keys = [signedmulti1, signedmulti2]
		# txDone = apply_multisignatures(tx, 0, self.lockingScript, keys)
		#print(txDone)
def mainMenu():
	player = Player()
	print("1. Cardio Goal\n2. Strength Goal")
	ResponseActivity = raw_input("select Activity: ")
	player.setActivity(ResponseActivity)
	goal = raw_input("Enter Goal: ")
	player.setGoal(goal)
	Reward = raw_input("Enter Reward Amount(Satoshis): ")
	player.setWager(Reward)
	return player

main()
#main()




