execute unless data storage glm:api/interpreter/function execute.args[0].value[] run return -1

data modify storage glm:interpreter temp.expected set from storage glm:api/interpreter/function execute.args[1].value[0]
data modify storage glm:interpreter temp.actual set from storage glm:api/interpreter/function execute.args[0].value[0]

execute store result score $check glm.interpreter run data modify storage glm:interpreter temp.actual set from storage glm:interpreter temp.expected

execute unless score $check glm.interpreter matches 0 run return -1

data remove storage glm:api/interpreter/function execute.args[0].value[0]
data remove storage glm:api/interpreter/function execute.args[1].value[0]

execute if data storage glm:api/interpreter/function execute.args[1].value[] run function glm:interpreter/evaluate/function/builtin/prefix/iterate
