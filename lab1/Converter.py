class Converter:
    @classmethod
    def convert(cls, number: str, p1: int, p2: int) -> str:
        if '.' in number:
            int_part, frac_part = number.split('.')
        else:
            int_part, frac_part = number, '0'
        
        int_part_base10 = cls._convert_to_ten(int_part, p1)

        frac_part_base10 = cls._convert_to_ten(f"0.{frac_part}", p1)

        int_result = cls._convert_from_ten(int(int_part_base10), p2)
        frac_result = cls._convert_fraction_from_ten(frac_part_base10, p2)
        
        if frac_result:
            return f"{int_result}.{frac_result}"
        return int_result

    @staticmethod
    def _convert_to_ten(number: str, p1: int) -> float:
        if '.' in number:
            int_part, frac_part = number.split('.')
        else:
            int_part, frac_part = number, '0'
        

        int_value = 0

        for i, digit in enumerate(int_part):
            if digit.isnumeric():
                int_value += int(digit) * (p1 ** (len(int_part)-i-1))
            else:
                int_value += (ord(digit)-55) * (p1 ** (len(int_part)-i-1))
        
        frac_value = 0

        for i, digit in enumerate(frac_part):
            if digit.isnumeric():
                frac_value += int(digit) * (p1 ** -(i + 1))
            else:
                frac_value += (ord(digit)-55) * (p1 ** -(i + 1))
        
        return int_value + frac_value


    @staticmethod
    def _convert_from_ten(number: int, p2: int) -> str:
        # Перевод целой части из десятичной системы в целевую
        result = ''
        
        if number == 0:
            return "0"
        
        while number > 0:
            if (number % p2) < 10:
                digit = str(number % p2)
            else:
                digit = chr(number % p2 + 55)
            
            result = digit+result
            number //= p2

        return result

    @staticmethod
    def _convert_fraction_from_ten(fraction: float, p2: int, precision: int = 10) -> str:
        # Перевод дробной части из десятичной системы в целевую
        result = []
        fraction_in_base10 = fraction
        for _ in range(precision):
            fraction_in_base10 *= p2
            digit = int(fraction_in_base10)
            result.append(str(digit))
            fraction_in_base10 -= digit
            if fraction_in_base10 == 0:
                break
        return ''.join(result)