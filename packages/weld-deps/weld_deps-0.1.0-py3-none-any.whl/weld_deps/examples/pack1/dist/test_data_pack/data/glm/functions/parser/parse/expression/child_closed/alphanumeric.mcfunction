data modify storage glm:parser temp.filter set value ["t","r","u","e"]
execute store result score $check glm.parser run data modify storage glm:parser temp.filter set from storage glm:parser parsed.value

execute if score $check glm.parser matches 0 run data modify storage glm:parser parsed set value {type:"literal",variant:"boolean",value:true}
execute if score $check glm.parser matches 0 run return -1

data modify storage glm:parser temp.filter set value ["f","a","l","s","e"]
execute store result score $check glm.parser run data modify storage glm:parser temp.filter set from storage glm:parser parsed.value

execute if score $check glm.parser matches 0 run data modify storage glm:parser parsed set value {type:"literal",variant:"boolean",value:false}
execute if score $check glm.parser matches 0 run return -1

data modify storage glm:parser parsed.variant set value "variable"
