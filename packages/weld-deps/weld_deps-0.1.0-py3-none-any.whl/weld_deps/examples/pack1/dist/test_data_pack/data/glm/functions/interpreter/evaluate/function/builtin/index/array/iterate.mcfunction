data modify storage glm:interpreter check_equality.a set from storage glm:api/interpreter/function execute.args[1]
data modify storage glm:interpreter check_equality.b set from storage glm:api/interpreter/function execute.args[0].value[0]
function glm:interpreter/utils/check_equality
execute if data storage glm:interpreter check_equality{result:true} store result storage glm:api/interpreter/function execute.return.value int 1 run scoreboard players get $index glm.interpreter
execute if data storage glm:interpreter check_equality{result:true} run return -1

data remove storage glm:api/interpreter/function execute.args[0].value[0]
scoreboard players add $index glm.interpreter 1
execute if data storage glm:api/interpreter/function execute.args[0].value[] run function glm:interpreter/evaluate/function/builtin/index/array/iterate
