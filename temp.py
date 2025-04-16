result = 1;
for (let i = 1; i <= 4; i++) {
    for (let j = 1; j <= i; j++) {
        result *= i - j + 1;
    }
}
console.log(result);