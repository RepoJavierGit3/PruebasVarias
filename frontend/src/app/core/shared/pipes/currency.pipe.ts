import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'currency'
})
export class CurrencyPipe implements PipeTransform {
  transform(value: number | string, currencyCode: string = 'USD'): string {
    if (value === null || value === undefined) return '';
    
    const numValue = typeof value === 'string' ? parseFloat(value) : value;
    
    if (isNaN(numValue)) return '';
    
    // Format based on currency code
    switch (currencyCode.toUpperCase()) {
      case 'USD':
      case 'CAD':
        return `$${numValue.toFixed(2)}`;
      case 'EUR':
        return `€${numValue.toFixed(2)}`;
      case 'GBP':
        return `£${numValue.toFixed(2)}`;
      case 'MXN':
        return `$${numValue.toFixed(2)} MXN`;
      default:
        return `${numValue.toFixed(2)} ${currencyCode}`;
    }
  }
}
