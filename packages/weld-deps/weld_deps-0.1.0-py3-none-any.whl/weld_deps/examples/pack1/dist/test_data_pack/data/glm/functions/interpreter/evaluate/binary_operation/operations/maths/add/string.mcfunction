execute unless data storage glm:interpreter evaluate.stack[-1].b{type:"literal",variant:"string"} run data modify storage glm:interpreter error set value '["TypeError: Literal string cannot be coerced to ",{"storage":"glm:interpreter","nbt":"evaluate.stack[-1].b.variant"},"."'
execute unless data storage glm:interpreter evaluate.stack[-1].b{type:"literal",variant:"string"} run return -1

data modify storage glm:interpreter evaluate.operation.result set from storage glm:interpreter evaluate.stack[-1].a
data modify storage glm:interpreter evaluate.operation.result.value append from storage glm:interpreter evaluate.stack[-1].b.value[]