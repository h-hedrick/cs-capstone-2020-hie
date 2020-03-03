import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-new-login-component',
  templateUrl: '../app.component.html', //surely we should be calling <login> on init?
  styleUrls: ['./new-login-component.component.css']
})
export class NewLoginComponentComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

}
