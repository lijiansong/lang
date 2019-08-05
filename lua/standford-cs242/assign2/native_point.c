#define LUA_LIB
#define _GNU_SOURCE

#include <lua.h>
#include <lauxlib.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

typedef struct {
  lua_Number x;
  lua_Number y;
} point_t;

static int point_add(lua_State* L) {
    // Your code here.
    point_t* p1 = (point_t*) luaL_checkudata(L, 1, "point_native");
    point_t* p2 = (point_t*) luaL_checkudata(L, 2, "point_native");
    
    point_t* point = (point_t*) lua_newuserdata(L, sizeof(point_t));
    luaL_getmetatable(L, "point_native");
    lua_setmetatable(L, -2);
    point->x = p1->x + p2->x;
    point->y = p1->y + p2->y;
    return 1;
}

static int point_dist(lua_State* L) {
    // Your code here.
    point_t* p1 = (point_t*) luaL_checkudata(L, 1, "point_native");
    point_t* p2 = (point_t*) luaL_checkudata(L, 2, "point_native");
    double x1 = p1->x;
    double x2 = p2->x;
    double dx = x1 - x2;
    double y1 = p1->y;
    double y2 = p2->y;
    double dy = y1 - y2;
    double dis = sqrt(dx * dx + dy * dy);
    lua_pushnumber(L, (lua_Number)dis);
    return 1;
}

static int point_eq(lua_State* L) {
    // Your code here.
    point_t* p1 = (point_t*) luaL_checkudata(L, 1, "point_native");
    point_t* p2 = (point_t*) luaL_checkudata(L, 2, "point_native");
    double x1 = p1->x;
    double x2 = p2->x;
    double y1 = p1->y;
    double y2 = p2->y;
    if(x1 == x2 && y1 == y2) {
        lua_pushboolean(L, 1);
    } else {
        lua_pushboolean(L, 0);
    }
    return 1;
}


static int point_sub(lua_State* L) {
    // Your code here.
    point_t* p1 = (point_t*) luaL_checkudata(L, 1, "point_native");
    point_t* p2 = (point_t*) luaL_checkudata(L, 2, "point_native");
    double x1 = p1->x;
    double x2 = p2->x;
    double dx = x1 - x2;
    double y1 = p1->y;
    double y2 = p2->y;
    double dy = y1 - y2;
    
    point_t* p = (point_t*) lua_newuserdata(L, sizeof(point_t));
    luaL_getmetatable(L, "point_native");
    lua_setmetatable(L, -2);
    p->x = (lua_Number) dx;
    p->y = (lua_Number) dy;
    return 1;
}

static int point_x(lua_State* L) {
    // Your code here.
    point_t* p = (point_t*) luaL_checkudata(L, 1, "point_native");
    double x = p->x;
    lua_pushnumber(L, (lua_Number)x);
    return 1;
}

static int point_y(lua_State* L) {
    // Your code here.
    point_t* p = (point_t*) luaL_checkudata(L, 1, "point_native");
    double y = p->y;
    lua_pushnumber(L, (lua_Number)y);
    return 1;
}

static int point_setx(lua_State* L) {
    // Your code here.
    point_t* p = (point_t*) luaL_checkudata(L, 1, "point_native");
    double new_x = lua_tonumber(L, 2);
    p->x = (lua_Number) new_x;
    return 0;
}

static int point_sety(lua_State* L) {
    // Your code here.
    point_t* p = (point_t*) luaL_checkudata(L, 1, "point_native");
    double new_y = lua_tonumber(L, 2);
    p->y = (lua_Number) new_y;
    return 0;
}

static int point_new(lua_State* L) {
    // Your code here.
    lua_Number x = lua_tonumber(L, 1);
    lua_Number y = lua_tonumber(L, 2);
    point_t* p = (point_t*) lua_newuserdata(L, sizeof(point_t));
    luaL_getmetatable(L, "point_native");
    lua_setmetatable(L, -2);
    p->x = x;
    p->y = y;
    return 1;
}

static int point_tostring(lua_State* L) {
    // Your code here. 
    point_t* p = (point_t*) luaL_checkudata(L, 1, "point_native");
    char* ch;
    int size = asprintf(&ch, "{%.f, %.f}", p->x, p->y);
    lua_pushstring(L, ch);
    return 1;
}

int luaopen_native_point(lua_State* L) {
  // Create the metatable that describes the behaviour of every point object.
  luaL_newmetatable(L, "point_native");

  // Add _, -, =, and tostring metamethods.
  {
    lua_pushstring(L, "__add");
    lua_pushcfunction(L, point_add);
    lua_settable(L, -3);

    lua_pushstring(L, "__sub");
    lua_pushcfunction(L, point_sub);
    lua_settable(L, -3);

    lua_pushstring(L, "__eq");
    lua_pushcfunction(L, point_eq);
    lua_settable(L, -3);

    lua_pushstring(L, "__tostring");
    lua_pushcfunction(L, point_tostring);
    lua_settable(L, -3);
  }

  // Create class table with a new method.
  lua_createtable(L, 1, 0);
  lua_pushstring(L, "new");
  lua_pushcfunction(L, point_new);
  lua_settable(L, -3);

  // Add Dist, X, Y, SetX, and SetY methods to class table.
  {
    lua_pushstring(L, "Dist");
    lua_pushcfunction(L, point_dist);
    lua_settable(L, -3);

    lua_pushstring(L, "X");
    lua_pushcfunction(L, point_x);
    lua_settable(L, -3);

    lua_pushstring(L, "Y");
    lua_pushcfunction(L, point_y);
    lua_settable(L, -3);

    lua_pushstring(L, "SetX");
    lua_pushcfunction(L, point_setx);
    lua_settable(L, -3);

    lua_pushstring(L, "SetY");
    lua_pushcfunction(L, point_sety);
    lua_settable(L, -3);
  }

  // Set the class table to the point metatable's __index.
  lua_pushstring(L, "__index");
  lua_pushvalue(L, -2);
  lua_settable(L, -4);

  // Only return one value at the top of the stack, which is the Point class
  // table.
  return 1;
}
