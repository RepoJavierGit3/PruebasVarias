import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'search'
})
export class SearchPipe implements PipeTransform {
  transform(items: any[], searchText: string, field: string = ''): any[] {
    if (!items) return [];
    if (!searchText) return items;
    
    searchText = searchText.toLowerCase();
    
    return items.filter(item => {
      if (field) {
        return item[field] && item[field].toString().toLowerCase().includes(searchText);
      } else {
        // Search in all string properties
        return Object.keys(item).some(key => {
          return item[key] && 
                 typeof item[key] === 'string' && 
                 item[key].toLowerCase().includes(searchText);
        });
      }
    });
  }
}
