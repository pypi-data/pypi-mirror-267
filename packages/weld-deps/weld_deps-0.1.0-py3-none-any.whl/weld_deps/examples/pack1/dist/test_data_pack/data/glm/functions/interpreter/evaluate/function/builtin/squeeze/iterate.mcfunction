execute store result score $check glm.interpreter run data modify storage glm:interpreter temp.last set from storage glm:api/interpreter/function execute.args[0].value[0]
execute if data storage glm:api/interpreter/function execute.args[1].value[] run function glm:interpreter/evaluate/function/builtin/squeeze/filter

execute if score $check glm.interpreter matches 1.. run data modify storage glm:api/interpreter/function execute.return.value append from storage glm:api/interpreter/function execute.args[0].value[0]

data remove storage glm:api/interpreter/function execute.args[0].value[0]
execute if data storage glm:api/interpreter/function execute.args[0].value[] run function glm:interpreter/evaluate/function/builtin/squeeze/iterate