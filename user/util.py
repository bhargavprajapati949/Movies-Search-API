# Password should be of Minimum eight characters, 
#   at least one uppercase letter, 
#   one lowercase letter, 
#   one number and 
#   one special character (@$!%*#?&)

registerReqSchema = {
    "type": "object",
    "properties": {
      "name": { 
        "type": "string",
        "minLength" : 1
      },
      "email": {
         "type": "string",
         "format": "idn-email"
      },
      "password": {
        "type": "string",
        "pattern": "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
      }
    },
    "required": ["name", "email", "password"],
     "additionalProperties": False
}

signInReqSchema = {
  "type": "object",
    "properties": {
      "email": { "type": "string" },
      "password": { "type": "string" }
    },
    "required": ["email", "password"],
     "additionalProperties": False
}