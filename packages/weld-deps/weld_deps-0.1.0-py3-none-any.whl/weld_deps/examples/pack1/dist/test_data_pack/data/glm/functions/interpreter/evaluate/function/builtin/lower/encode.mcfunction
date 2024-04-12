data modify storage moxlib:api/string/ascii/encode target set from storage glm:api/interpreter/function execute.args[0].value[0]

function moxlib:api/string/ascii/encode
execute store result score $char glm.interpreter run data get storage moxlib:api/string/ascii/encode output

execute unless score $char glm.interpreter matches 65..90 run data modify storage glm:api/interpreter/function execute.return.value append from storage glm:api/interpreter/function execute.args[0].value[0]
execute unless score $char glm.interpreter matches 65..90 run return -1

execute store result storage moxlib:api/string/ascii/decode target int 1 run scoreboard players add $char glm.interpreter 32
function moxlib:api/string/ascii/decode
data modify storage glm:api/interpreter/function execute.return.value append from storage moxlib:api/string/ascii/decode output