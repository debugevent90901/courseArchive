#include "RationalNumber.h"

//to_String converts numerator and denominator to string of type num/denom
string RationalNumber::to_String(void){
	stringstream my_output;
	my_output << numerator << "/" << denominator;
	return my_output.str();
}

int gcd(int a, int b)
{
	int tmp;
	if ( a - b >= 0 )
	{
		tmp = a % b;
		if ( 0 == tmp )
			return b;
		else
			return gcd(tmp, b); 
	}
	else
		return gcd(b, a);
}

RationalNumber::RationalNumber() { NumberType = RATIONAL; numerator = 0; denominator = 1; }

RationalNumber::RationalNumber(int numer, int denom) { NumberType = RATIONAL; numerator = numer; denominator = denom; }

void RationalNumber::set_numerator(int numer)
{
	int tmp = RationalNumber::gcd(numer, denominator);
 	numerator = numer / tmp;
 	denominator /= tmp; 
}

void RationalNumber::set_denominator(int denom) 
{ 
	int tmp = RationalNumber::gcd(denom, numerator);
 	numerator /= tmp;
	denominator = denom / tmp;
}

int RationalNumber::get_numerator(void) const { return numerator; }

int RationalNumber::get_denominator(void) const { return denominator; }

void RationalNumber::set_value (int numer, int denom) 
{ 
	int tmp = RationalNumber::gcd(denom, numer);
 	numerator = numer / tmp;
	denominator = denom / tmp;
}

double RationalNumber::magnitude()
{
	return (double(numerator) / double(denominator) < 0) ? (-double(numerator) / double(denominator)) : double(numerator) / double(denominator);
}

double RationalNumber::decimal_value() const 
{
	return double(numerator) / double(denominator);
}

RationalNumber RationalNumber::operator + (const RationalNumber& arg)
{
	return RationalNumber(this->numerator * arg.denominator + this->denominator * arg.numerator, this->denominator * arg.denominator);
}

RationalNumber RationalNumber::operator - (const RationalNumber& arg)
{
	return RationalNumber(this->numerator * arg.denominator - this->denominator * arg.numerator, this->denominator * arg.denominator);
}

RationalNumber RationalNumber::operator * (const RationalNumber& arg)
{
	return RationalNumber(this->numerator * arg.numerator, this->denominator * arg.denominator);
}

RationalNumber RationalNumber::operator / (const RationalNumber& arg)
{
	return RationalNumber(this->numerator * arg.denominator, this->denominator * arg.numerator);
}

ComplexNumber RationalNumber::operator + (const ComplexNumber& arg)
{
	return ComplexNumber(this->decimal_value() + arg.get_realComponent(), arg.get_imagComponent());	
}
	
ComplexNumber RationalNumber::operator - (const ComplexNumber& arg)
{
	return ComplexNumber(this->decimal_value() - arg.get_realComponent(), arg.get_imagComponent());
}

ComplexNumber RationalNumber::operator * (const ComplexNumber& arg)
{
	return ComplexNumber(this->decimal_value() * arg.get_realComponent(), this->decimal_value() * arg.get_imagComponent());
}

ComplexNumber RationalNumber::operator / (const ComplexNumber& arg)
{
	return ComplexNumber(this->decimal_value() * arg.get_realComponent() / (arg.get_realComponent() * arg.get_realComponent() + arg.get_imagComponent() * arg.get_imagComponent()) , -1 * this->decimal_value() * arg.get_imagComponent() / (arg.get_realComponent() * arg.get_realComponent() + arg.get_imagComponent() * arg.get_imagComponent()));
}

RealNumber RationalNumber::operator + (const RealNumber& arg)
{
	return RealNumber(this->decimal_value() + arg.get_value());
}

RealNumber RationalNumber::operator - (const RealNumber& arg)
{
	return RealNumber(this->decimal_value() - arg.get_value());
}

RealNumber RationalNumber::operator * (const RealNumber& arg)
{
	return RealNumber(this->decimal_value() * arg.get_value());
}

RealNumber RationalNumber::operator / (const RealNumber& arg)
{
	return RealNumber(this->decimal_value() / arg.get_value());
}

































