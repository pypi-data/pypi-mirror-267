execute store result score .different glm.interpreter run data modify storage glm:interpreter check_equality.a set from storage glm:interpreter check_equality.b
execute if score .different glm.interpreter matches 0 run data modify storage glm:interpreter check_equality.result set value true
execute if score .different glm.interpreter matches 1 run data modify storage glm:interpreter check_equality.result set value false
