import React from "react";
import { Link } from "react-router-dom";

export default function MainNav() {
  const navLinks = [
    {
      label: "New Arrivals",
      href: "/products",
    },
    {
      label: "Tops",
      href: "/products",
    },
    {
      label: "Bottoms",
      href: "/products",
    },
    {
      label: "Shoes",
      href: "/products",
    },
    {
      label: "Sale",
      href: "/products",
    },
  ];
  return (
    <nav id="main-nav">
      <ul>
        {navLinks.map((link) => (
          <li key={link.label}>
            <Link to={link.href}>{link.label}</Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}
