import React from 'react';
import './skeleton.css';

export default function SkeletonBlock({ width='100%', height=16 }){
  return <div className="skeleton" style={{width, height}} aria-hidden="true" />;
}