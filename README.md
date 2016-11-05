# MMeTokenDecrypt
This program decrypts / extracts all authorization tokens on macOS / OS X / OSX. No user authentication is needed, due to the flawed way in which macOS authorizes keychain access.

Authorization tokens are stored in `/Users/*/Library/Application Support/iCloud/Accounts/DSID` where DSID is Apple's backend identifier for each iCloud account in their system. 

This `DSID` file is encrypted with `AES-128 CBC` and an empty `intialization vector` (IV). The decryption key for this file is stored in the User's `keychain`, under the service name entry `iCloud`, with the name being the primary email address associated with an iCloud account.

This `decryption key` is decoded in base64, and then used as the message in a standard `MD5 Hmac`. The problem is, the key to the Hmac is buried deep in the `internals of MacOS`. This key is a 44 character long string of random letters that is necessary to decrypt the DSID file. This key is included in the source code of this repository, and as far as I know, has been published no where else on the internet.

## Significance

The only software that performs a similar function is the forensics grade "Elcomsoft Phone Breaker". MMeTokenDecrypt allows any developer to incorporate the decryption of iCloud authorization files into their projects, open sourced.

Apple needs to redesign the way that keychain information is requested. Because this program forks a security subprocess, which is an Apple signed binary, the user is not alerted to the potential dangerous nature of the keychain request dialog. Additionally, an attacker can repeatedly present the user with the keychain dialog, until the user accepts the keychain request, because Apple does not put a timeout on the "deny" attempts. This allows for trivial compromization of iCloud authorization tokens, which can be used to access almost every iCloud service, including `iOS backups, iCloud Contacts, iCloud Drive, iCloud Photo Library, Find my Friends, and Find my iPhone`. 

---
## Usage

```
python MMeDecrypt.py
```

```
Decrypting token plist -> [/Users/bob/Library/Application Support/iCloud/Accounts/123456789]

Successfully decrypted token plist!

bobloblaw@gmail.com Bob Loblaw -> [123456789]

cloudKitToken = AQAAAABYXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX~

mapsToken = AQAAAAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX~

mmeAuthToken = AQAAAABXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX=

mmeBTMMInfiniteToken = AQAAAABXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX~

mmeFMFAppToken = AQAAAABXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX~

mmeFMIPToken = AQAAAABXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX~
```
