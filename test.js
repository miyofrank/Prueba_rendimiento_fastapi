import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 10, // usuarios virtuales
  stages: [    
    { duration: "10s", target: 10 }, // Sube a 10 usuarios virtuales durante 10 segundos    
    { duration: "30s", target: 10 }, // Mantiene 10 usuarios durante 30 segundos    
    { duration: "10s", target: 0 }, // Baja gradualmente  
    ],
};


export default function () {
  let res = http.get('http://localhost:8000/tasks/1/calculate');
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
  sleep(1);
}
