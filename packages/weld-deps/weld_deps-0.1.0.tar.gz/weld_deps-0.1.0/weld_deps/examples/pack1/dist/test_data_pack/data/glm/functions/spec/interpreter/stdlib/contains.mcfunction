function glm:spec/helpers/check {describes: "Successfully using contains on an array", expects: ["true"], receives: ["contains?(['hi','there'], 'hi')"]}
function glm:spec/helpers/check {describes: "Unsuccessfully using contains on an array", expects: ["false"], receives: ["contains?([true,undefined,/hi/], false)"]}
function glm:spec/helpers/check {describes: "Successfully using contains on a string", expects: ["true"], receives: ["contains?('kukuko', 'kuko')"]}
function glm:spec/helpers/check {describes: "Unsuccessfully using contains on a string", expects: ["false"], receives: ["contains?('Hi, what\\'s up?', 'q')"]}
