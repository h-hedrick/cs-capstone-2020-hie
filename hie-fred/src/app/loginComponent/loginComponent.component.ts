import { Component, OnInit } from '@angular/core';
import { componentFactoryName } from '@angular/compiler';

@Component({
  selector: 'loginComponent', // inject with <loginComponent>...</loginComponent>
  templateUrl: '../app.component.html', //surely we should be calling <login> on init? yes!
  styleUrls: ['./loginComponent.component.css']
})
export class loginComponent implements OnInit {

  title = 'loginComponent';

  constructor() { }

  ngOnInit(): void {
  }

}
