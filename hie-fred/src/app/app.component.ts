import { Component } from '@angular/core';

@Component({
  selector: 'app-root', //name of the <tag> that calls this component
  templateUrl: './app.component.html', //file where <app-root> can be found
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'hie-fred';
}
