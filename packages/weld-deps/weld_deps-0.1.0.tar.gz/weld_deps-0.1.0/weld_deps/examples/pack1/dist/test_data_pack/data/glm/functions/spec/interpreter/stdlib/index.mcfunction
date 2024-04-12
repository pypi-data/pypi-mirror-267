function glm:spec/helpers/check {describes: "Successfully indexing an array", expects: ["0"], receives: ["index([1,2,3], 1)"]}
function glm:spec/helpers/check {describes: "Unsuccessfully indexing an array", expects: ["-1"], receives: ["index([1,2,4], 3)"]}
function glm:spec/helpers/check {describes: "Successfully indexing a string", expects: ["2"], receives: ["index('hello', 'll')"]}
function glm:spec/helpers/check {describes: "Unsuccessfully indexing a string", expects: ["-1"], receives: ["index('foobarbaz', 'bag')"]}
