execute store result score $sleep_time glm.interpreter run data get storage glm:api/interpreter/function execute.args[0].value

execute store result storage glm:api/interpreter/function execute.args[0].value int 1 run scoreboard players remove $sleep_time glm.interpreter 1

execute if score $sleep_time glm.interpreter matches 1.. run data modify storage glm:interpreter evaluate.loop set value true
