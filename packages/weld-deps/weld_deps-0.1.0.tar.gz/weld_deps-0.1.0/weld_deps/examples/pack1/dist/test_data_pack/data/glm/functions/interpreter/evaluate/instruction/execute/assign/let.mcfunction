data modify storage glm:interpreter evaluate.variable.name set from storage glm:interpreter evaluate.stack[-1].evaluated_args[0]
data modify storage glm:interpreter evaluate.variable.value set from storage glm:interpreter evaluate.stack[-1].evaluated_args[1]
function glm:interpreter/evaluate/instruction/execute/assign/assign