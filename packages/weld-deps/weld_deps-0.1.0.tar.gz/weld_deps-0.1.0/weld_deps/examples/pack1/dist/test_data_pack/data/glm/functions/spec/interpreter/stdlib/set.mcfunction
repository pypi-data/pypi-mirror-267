function glm:spec/helpers/check {describes: "Setting in an array", expects: ["[1,2,4]"], receives: ["set([1,2,3], 2, 4)"]}
function glm:spec/helpers/check {describes: "Unsuccessfully setting in an array", expects: ["[1,2,3]"], receives: ["set([1,2,3], -105, 'foo')"]}
function glm:spec/helpers/check {describes: "Setting in an object", expects: ["{A:65,z:122}"], receives: ["set({A:65,z:121}, 'z', 122)"]}
function glm:spec/helpers/check {describes: "Creating a key in an object", expects: ["{A:65,z:122,_:95}"], receives: ["set({A:65,z:122}, '_', 95)"]}
function glm:spec/helpers/check {describes: "Setting in a string", expects: ["'Hi :)'"], receives: ["set('Hi :(', 4, ')')"]}
function glm:spec/helpers/check {describes: "Unsuccessfully setting in a string", expects: ["'foo'"], receives: ["set('foo', 82, '@')"]}

