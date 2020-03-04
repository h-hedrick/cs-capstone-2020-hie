import { Component, OnInit } from '@angular/core';
import { componentFactoryName } from '@angular/compiler';

@Component({
  selector: 'loginComponent', // inject with <loginComponent>...</loginComponent>
  templateUrl: './loginComponent.component.html',
  styleUrls: ['./loginComponent.component.css']
})
export class loginComponent implements OnInit {


  constructor() { }

  ngOnInit(): void {
  }

}
