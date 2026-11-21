import React from "react";
import Cart from "../cart/Cart";
import SideDrawer from "../modal/SideDrawer/SideDrawer";
import { Link } from "react-router-dom";

export default function SubNav() {
  return (
    <nav id="sub-nav">
      <ul>
        <li><Link to="/register">Register</Link></li>
        <li>Free Shipping on Orders Over US$ 100</li>
        <div className="flex gap-4 items-center">
          <li><Link to="/login">Login</Link></li>
          <Cart/>
        </div>
      </ul>
    </nav>
  );
}
