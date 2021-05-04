#include "ComplexNumber.h"

//to_String converts real and imaginary components to string of type a+bi
string ComplexNumber::to_String(void){
	stringstream my_output;
	my_output << realComponent;
	if(imagComponent >= 0){
		my_output << " + " << imagComponent << "i";
	}
	else if(imagComponent < 0){
		my_output << "-" << imagComponent*(-1) << "i";
	}
	return my_output.str();
}

ComplexNumber::ComplexNumber() { NumberType = COMPLEX; realComponent = 0; imagComponent = 0; }

ComplexNumber::ComplexNumber(double real, double imag) { NumberType = COMPLEX; realComponent = real; imagComponent = imag; }

void ComplexNumber::set_realComponent(double rval) { realComponent = rval; }

void ComplexNumber::set_imagComponent(double ival) { imagComponent = ival; }

double ComplexNumber::get_realComponent(void) const { return realComponent; }

double ComplexNumber::get_imagComponent(void) const { return imagComponent; }

void ComplexNumber::set_value (double rval, double ival) { realComponent = rval; imagComponent = ival; }

double ComplexNumber::magnitude() { return sqrt(realComponent * realComponent + imagComponent * imagComponent); }

ComplexNumber ComplexNumber::operator + (const ComplexNumber& arg)
{
	return ComplexNumber(this->realComponent + arg.realComponent, this->imagComponent + arg.imagComponent);
}

ComplexNumber ComplexNumber::operator - (const ComplexNumber& arg)
{
	return ComplexNumber(this->realComponent - arg.realComponent, this->imagComponent - arg.imagComponent);
}

ComplexNumber ComplexNumber::operator * (const ComplexNumber& arg)
{
	return ComplexNumber(this->realComponent * arg.realComponent - this->imagComponent * arg.imagComponent, this->realComponent * arg.imagComponent + this->imagComponent * arg.realComponent);
}

ComplexNumber ComplexNumber::operator / (const ComplexNumber& arg)
{
	return ComplexNumber((this->realComponent * arg.realComponent + this->imagComponent * arg.imagComponent) / (arg.realComponent * arg.realComponent + arg.imagComponent * arg.imagComponent), (this->imagComponent * arg.realComponent - this->realComponent * arg.imagComponent) / (arg.realComponent * arg.realComponent + arg.imagComponent * arg.imagComponent));
}

ComplexNumber ComplexNumber::operator + (const RealNumber& arg)
{
	return ComplexNumber(this->realComponent + arg.get_value(), this->imagComponent);
}

ComplexNumber ComplexNumber::operator - (const RealNumber& arg)
{
	return ComplexNumber(this->realComponent - arg.get_value(), this->imagComponent);
}

ComplexNumber ComplexNumber::operator * (const RealNumber& arg)
{
	return ComplexNumber(this->realComponent * arg.get_value(), this->imagComponent * arg.get_value());
}

ComplexNumber ComplexNumber::operator / (const RealNumber& arg)
{
	return ComplexNumber(this->realComponent / arg.get_value(), this->imagComponent / arg.get_value());
}

ComplexNumber ComplexNumber::operator + (const RationalNumber& arg)
{
	return ComplexNumber(this->realComponent + arg.decimal_value(), this->imagComponent);
}

ComplexNumber ComplexNumber::operator - (const RationalNumber& arg)
{
	return ComplexNumber(this->realComponent - arg.decimal_value(), this->imagComponent);
}

ComplexNumber ComplexNumber::operator * (const RationalNumber& arg)
{
	return ComplexNumber(this->realComponent * arg.decimal_value(), this->imagComponent * arg.decimal_value());
}

ComplexNumber ComplexNumber::operator / (const RationalNumber& arg)
{
	return ComplexNumber(this->realComponent / arg.decimal_value(), this->imagComponent / arg.decimal_value());
}
