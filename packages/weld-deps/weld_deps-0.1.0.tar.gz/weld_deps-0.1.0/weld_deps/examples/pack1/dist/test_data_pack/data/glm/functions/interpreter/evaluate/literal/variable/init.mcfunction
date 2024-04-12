data modify storage moxlib:api/data/get key.name set from storage glm:interpreter evaluate.stack[-1].value
data modify storage moxlib:api/data/get target set from storage glm:interpreter variables

function moxlib:api/data/get

execute unless data storage moxlib:api/data/get {success:true} run data modify storage moxlib:api/data/get output.value set value {type:"undefined",value: false}

execute store result score $parameters glm.interpreter run data get storage glm:interpreter evaluate.stack[-1].parameters
execute if score $parameters glm.interpreter matches 0 run data modify storage glm:interpreter evaluate.stack[-1] set from storage moxlib:api/data/get output.value
execute if score $parameters glm.interpreter matches 0 run return -1

data modify storage moxlib:api/data/get output.value.parameters set from storage glm:interpreter evaluate.stack[-1].parameters
data modify storage moxlib:api/data/get output.value.metadata.status set value "closed"
data modify storage glm:interpreter evaluate.replace set from storage moxlib:api/data/get output.value