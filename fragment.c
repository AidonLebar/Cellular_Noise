#version 120
#define FLT_MAX 1.0/0.0
uniform float res;
uniform vec2 node[?];
uniform int r_nth;
uniform int g_nth;
uniform int b_nth;
uniform int r;
uniform int g;
uniform int b;
uniform int isolines;

float manhattan(vec2 p1, vec2 p2){
  return abs(p1.x - p2.x) + abs(p1.y - p2.y);
}

float canberra(vec2 p1, vec2 p2){
  return (abs(p1.x - p2.x)/(abs(p1.x) + abs(p2.x)) + abs(p1.y - p2.y)/(abs(p1.y) + abs(p2.y)))/2.0;
}

float chebyshev(vec2 p1, vec2 p2){
  float d = abs(p1.x - p2.x);
  d = max(d, abs(p1.y - p2.y));
  return d;
}

float euclidean(vec2 p1, vec2 p2){
  return distance(p1, p2);
}

float third_power(vec2 p1, vec2 p2){
  return pow(pow(abs(p1.x-p2.x), 3) + pow(abs(p1.y-p2.y), 3), 0.3333);
}

float forth_power(vec2 p1, vec2 p2){
  return pow(pow(abs(p1.x-p2.x), 4) + pow(abs(p1.y-p2.y), 4), 0.25);
}

float half_power(vec2 p1, vec2 p2){
  return pow(pow(abs(p1.x-p2.x), 0.5) + pow(abs(p1.y-p2.y), 0.5), 2);
}

float negative_power(vec2 p1, vec2 p2){
  return pow(pow(abs(p1.x-p2.x), -0.5) + pow(abs(p1.y-p2.y), -0.5), -2);
}

float knights(vec2 p1, vec2 p2){
  float x = abs(p1.x - p2.x);
  float y = abs(p1.y - p2.y);
  if (x < y) {
    float t = x;
    x = y;
    y = t;
  }
  if(x == 1.0/res && y == 0){
    return 3.0/res;
  }
  if(x == 2.0/res && y == 2.0/res){
    return 4.0/res;
  }
  float del = x - y;
  if(y > del){
    return del - 2*((del-y)/3.0);
  }
  else{
    return del - 2*((del-y)/4.0);
  }
}

float iron_cross(vec2 p1, vec2 p2){
  float x = abs(p1.x - p2.x);
  float y = abs(p1.y - p2.y);
  if (x < y) {
    float t = x;
    x = y;
    y = t;
  }
  if(x == 1.0/res && y == 0){
    return 3.0/res;
  }
  if(x == 2.0/res && y == 2.0/res){
    return 4.0/res;
  }
  float del = x - y;
  if(y > del){
    return del - 2*floor((del-y)/3.0);
  }
  else{
    return del - 2*floor((del-y)/4.0);
  }
}

float octagon(vec2 p1, vec2 p2){
  return manhattan(p1, p2) + chebyshev(p1, p2);
}

float mod_euclidean(vec2 p1, vec2 p2){
  return mod(int(distance(p1, p2) * res), 500 )/res;
}

float mod_octagon(vec2 p1, vec2 p2){
  return mod(int(octagon(p1, p2) * res), 500 )/res;
}

float mod_manhattan(vec2 p1, vec2 p2){
  return mod(int(manhattan(p1, p2) * res), 500 )/res;
}

void main(){
  float d;
  float m[3] = float[3](FLT_MAX, FLT_MAX, FLT_MAX);
  for(int i = 0; i < ?; i++){
    d = METRIC_FUNC(gl_FragCoord.xy/res, node[i]);
    if(d < m[0]){
      m[2] = m[1];
      m[1] = m[0];
      m[0] = d;
    }
    else if(d < m[1]){
      m[2] = m[1];
      m[1] = d;
    }
    else if(d < m[2]){
      m[2] = d;
    }
  }
  
  if(isolines > 0){
    m[0] -= step(.7,abs(sin(150.0*m[0])))*.3;
    m[1] -= step(.7,abs(sin(150.0*m[1])))*.3;
    m[2] -= step(.7,abs(sin(150.0*m[2])))*.3;
  }
  gl_FragColor = vec4(r*m[r_nth], g*m[g_nth], b*m[b_nth], 1);
}
