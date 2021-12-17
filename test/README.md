# CyPress Test Suite for INCIPIT-CRIS

## Installation

- `git clone https://github.com/HEG-INCIPIT/INCIPIT-CRIS.git`
- `cd test`
- `npm install`
- Copy the `cypress.env.json.dist` to `cypress.env.json`
  - And edit it to the correct value
- `npm run cypress` (This will install the missing cypress elements)

## Usage

- `npm run cypress` will launch the GUI
- `npm run test` will run the tests on the CLI

## Environment Variables

You can set the variable in the `cypress.env.json(.dist)` file as env variable in bash (or secrets,...) like this:

For
```javascript
"cris_account": {
    "account1": {
        "username": "username1",
        "password": "password1",
    },
},
```
You have to write it like that:

```bash
export cypress_cris_account='"account1": {"username": "username1","password": "password1",}'
```

Cypress will correctly load the JS Object.
