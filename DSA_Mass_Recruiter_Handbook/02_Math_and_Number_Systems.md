# Math & Number Systems — Q41 to Q55

> **Target companies:** TCS (highest focus), Wipro, HCL  
> **Difficulty:** Easy to Medium  
> **Coverage:** ~15% of mass-recruiter questions — TCS NQT tests number-system conversions very heavily

---

## Q41. Decimal to Binary Conversion

**Problem:** Convert a decimal integer to its binary representation.  
**Companies:** TCS (very frequent), Wipro  
**Approach:** Repeatedly divide by 2 and collect remainders.

```java
public class DecimalToBinary {
    public static String decToBin(int n) {
        if (n == 0) return "0";
        StringBuilder sb = new StringBuilder();
        while (n > 0) {
            sb.append(n % 2);
            n /= 2;
        }
        return sb.reverse().toString();
    }

    public static void main(String[] args) {
        System.out.println(decToBin(10));  // 1010
        System.out.println(decToBin(255)); // 11111111
    }
}
```
**Time:** O(log n) | **Space:** O(log n)

---

## Q42. Binary to Decimal Conversion

**Problem:** Convert a binary string to its decimal equivalent.  
**Companies:** TCS, HCL  

```java
public class BinaryToDecimal {
    public static int binToDec(String binary) {
        int result = 0, power = 1;
        for (int i = binary.length() - 1; i >= 0; i--) {
            result += (binary.charAt(i) - '0') * power;
            power *= 2;
        }
        return result;
    }

    public static void main(String[] args) {
        System.out.println(binToDec("1010"));     // 10
        System.out.println(binToDec("11111111")); // 255
    }
}
```
**Time:** O(n) | **Space:** O(1)

---

## Q43. Decimal to Hexadecimal Conversion

**Problem:** Convert a decimal integer to hexadecimal without using Integer.toHexString().  
**Companies:** TCS  

```java
public class DecimalToHex {
    public static String decToHex(int n) {
        if (n == 0) return "0";
        char[] hexChars = "0123456789ABCDEF".toCharArray();
        StringBuilder sb = new StringBuilder();
        while (n > 0) {
            sb.append(hexChars[n % 16]);
            n /= 16;
        }
        return sb.reverse().toString();
    }

    public static void main(String[] args) {
        System.out.println(decToHex(255)); // FF
        System.out.println(decToHex(16));  // 10
    }
}
```
**Time:** O(log n) | **Space:** O(log n)

---

## Q44. Check if a Number is Prime

**Problem:** Determine if a given number is prime.  
**Companies:** TCS (very frequent), Wipro, HCL  
**Approach:** Check divisors up to √n.

```java
public class PrimeCheck {
    public static boolean isPrime(int n) {
        if (n < 2) return false;
        if (n == 2) return true;
        if (n % 2 == 0) return false;
        for (int i = 3; i * i <= n; i += 2)
            if (n % i == 0) return false;
        return true;
    }

    public static void main(String[] args) {
        System.out.println(isPrime(17)); // true
        System.out.println(isPrime(15)); // false
        System.out.println(isPrime(2));  // true
    }
}
```
**Time:** O(√n) | **Space:** O(1)

---

## Q45. Generate All Primes in a Range (Sieve of Eratosthenes)

**Problem:** Print all prime numbers up to n.  
**Companies:** TCS, Wipro  
**Approach:** Sieve — mark multiples of each prime as composite.

```java
import java.util.*;

public class SieveOfEratosthenes {
    public static List<Integer> sieve(int n) {
        boolean[] isComposite = new boolean[n + 1];
        List<Integer> primes = new ArrayList<>();
        for (int i = 2; i <= n; i++) {
            if (!isComposite[i]) {
                primes.add(i);
                for (long j = (long) i * i; j <= n; j += i)
                    isComposite[(int) j] = true;
            }
        }
        return primes;
    }

    public static void main(String[] args) {
        System.out.println(sieve(30)); // [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    }
}
```
**Time:** O(n log log n) | **Space:** O(n)

---

## Q46. Digit Sum of a Number

**Problem:** Find the sum of all digits of a given number.  
**Companies:** TCS, Wipro, HCL  

```java
public class DigitSum {
    public static int digitSum(int n) {
        n = Math.abs(n);
        int sum = 0;
        while (n > 0) {
            sum += n % 10;
            n /= 10;
        }
        return sum;
    }

    public static void main(String[] args) {
        System.out.println(digitSum(1234));  // 10
        System.out.println(digitSum(-9876)); // 30
    }
}
```
**Time:** O(digits) | **Space:** O(1)

---

## Q47. Reverse a Number

**Problem:** Reverse the digits of an integer.  
**Companies:** TCS, Wipro, HCL  

```java
public class ReverseNumber {
    public static long reverse(int n) {
        long reversed = 0;
        boolean isNegative = n < 0;
        n = Math.abs(n);
        while (n > 0) {
            reversed = reversed * 10 + n % 10;
            n /= 10;
        }
        return isNegative ? -reversed : reversed;
    }

    public static void main(String[] args) {
        System.out.println(reverse(12345));  // 54321
        System.out.println(reverse(-9876));  // -6789
    }
}
```
**Time:** O(digits) | **Space:** O(1)

---

## Q48. Check Armstrong Number

**Problem:** A number is Armstrong if the sum of its digits raised to the power of the number of digits equals the number itself. e.g., 153 = 1³ + 5³ + 3³.  
**Companies:** TCS (very frequent), HCL  

```java
public class ArmstrongNumber {
    public static boolean isArmstrong(int n) {
        String s = String.valueOf(n);
        int power = s.length(), sum = 0;
        for (char c : s.toCharArray())
            sum += (int) Math.pow(c - '0', power);
        return sum == n;
    }

    public static void main(String[] args) {
        System.out.println(isArmstrong(153));  // true (1^3 + 5^3 + 3^3 = 153)
        System.out.println(isArmstrong(9474)); // true (9^4 + 4^4 + 7^4 + 4^4 = 9474)
        System.out.println(isArmstrong(100));  // false
    }
}
```
**Time:** O(digits) | **Space:** O(1)

---

## Q49. GCD (Greatest Common Divisor) of Two Numbers

**Problem:** Find the GCD of two numbers.  
**Companies:** TCS, Wipro  
**Approach:** Euclidean algorithm — gcd(a, b) = gcd(b, a % b).

```java
public class GCD {
    public static int gcd(int a, int b) {
        while (b != 0) {
            int t = b;
            b = a % b;
            a = t;
        }
        return a;
    }

    public static void main(String[] args) {
        System.out.println(gcd(48, 18)); // 6
        System.out.println(gcd(56, 98)); // 14
    }
}
```
**Time:** O(log(min(a,b))) | **Space:** O(1)

---

## Q50. LCM (Lowest Common Multiple) of Two Numbers

**Problem:** Find the LCM of two numbers.  
**Companies:** TCS, HCL  
**Approach:** LCM(a, b) = (a / GCD(a, b)) * b (dividing first to avoid overflow).

```java
public class LCM {
    static int gcd(int a, int b) {
        return b == 0 ? a : gcd(b, a % b);
    }

    public static long lcm(int a, int b) {
        return (long)(a / gcd(a, b)) * b;
    }

    public static void main(String[] args) {
        System.out.println(lcm(4, 6));   // 12
        System.out.println(lcm(15, 20)); // 60
    }
}
```
**Time:** O(log(min(a,b))) | **Space:** O(1)

---

## Q51. Check if a Number is Perfect

**Problem:** A perfect number equals the sum of its proper divisors (excluding itself). e.g., 28 = 1+2+4+7+14.  
**Companies:** TCS  

```java
public class PerfectNumber {
    public static boolean isPerfect(int n) {
        if (n < 2) return false;
        int sum = 1;
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                sum += i;
                if (i != n / i) sum += n / i;
            }
        }
        return sum == n;
    }

    public static void main(String[] args) {
        System.out.println(isPerfect(28)); // true
        System.out.println(isPerfect(6));  // true
        System.out.println(isPerfect(12)); // false
    }
}
```
**Time:** O(√n) | **Space:** O(1)

---

## Q52. Power of a Number (Fast Exponentiation)

**Problem:** Calculate x raised to the power n efficiently.  
**Companies:** TCS, Wipro  
**Approach:** Recursively square and halve — O(log n).

```java
public class PowerFunction {
    public static double myPow(double x, int n) {
        if (n == 0) return 1;
        if (n < 0) { x = 1 / x; n = -n; }
        if (n % 2 == 0) return myPow(x * x, n / 2);
        return x * myPow(x * x, n / 2);
    }

    public static void main(String[] args) {
        System.out.println(myPow(2, 10));  // 1024.0
        System.out.println(myPow(2, -2));  // 0.25
    }
}
```
**Time:** O(log n) | **Space:** O(log n)

---

## Q53. Count Digits in a Number

**Problem:** Count the number of digits in an integer without converting to string.  
**Companies:** TCS, HCL  

```java
public class CountDigits {
    public static int countDigits(int n) {
        if (n == 0) return 1;
        n = Math.abs(n);
        int count = 0;
        while (n > 0) { count++; n /= 10; }
        return count;
    }

    public static void main(String[] args) {
        System.out.println(countDigits(12345)); // 5
        System.out.println(countDigits(0));     // 1
        System.out.println(countDigits(-999));  // 3
    }
}
```

---

## Q54. Sum of First N Natural Numbers

**Problem:** Return the sum of 1 to N without a loop (formula method) and verify with a loop.  
**Companies:** TCS, HCL, Tech Mahindra  

```java
public class SumNaturalNumbers {
    // O(1) formula
    public static long sumFormula(int n) {
        return (long) n * (n + 1) / 2;
    }

    // O(n) loop (to show you know both)
    public static long sumLoop(int n) {
        long sum = 0;
        for (int i = 1; i <= n; i++) sum += i;
        return sum;
    }

    public static void main(String[] args) {
        System.out.println(sumFormula(100)); // 5050
        System.out.println(sumLoop(100));    // 5050
    }
}
```

---

## Q55. Print Multiplication Table

**Problem:** Print the multiplication table of a given number up to 10.  
**Companies:** HCL, Tech Mahindra (interview warm-up)  

```java
public class MultiplicationTable {
    public static void printTable(int n) {
        System.out.println("Multiplication table of " + n + ":");
        for (int i = 1; i <= 10; i++)
            System.out.printf("%d x %d = %d%n", n, i, n * i);
    }

    public static void main(String[] args) {
        printTable(7);
    }
}
```

---

*Next: [03_Sorting_and_Searching.md](./03_Sorting_and_Searching.md)*
