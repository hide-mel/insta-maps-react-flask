import React, { useState, useRef } from 'react';
import * as FaIcons from 'react-icons/fa';
import * as AiIcons from 'react-icons/ai';
import './navbar.css';
import { IconContext } from 'react-icons';

const Navbar = (props) => {
    const [sidebar, setSidebar] = useState(false);
    const showSidebar = () => setSidebar(!sidebar);

    const usernameRef = useRef()
    const passRef = useRef()
    const targetRef = useRef()

    const handleSubmit = (e) => {
        e.preventDefault()  
        props.getData(usernameRef.current.value, passRef.current.value, targetRef.current.value)
        usernameRef.current.value = null
        passRef.current.value = null
        //targetRef.current.value = null
    }

  return (
    <>
        <IconContext.Provider value={{ color: '#fff' }}>
            <div className='navbar'>
                <FaIcons.FaBars onClick={showSidebar} className='menu-bars'/>
            </div>
            <nav className={sidebar ? 'nav-menu active' : 'nav-menu'}>
            <div className='nav-menu-items'>
                <div className='navbar-toggle'>
                    <AiIcons.AiOutlineClose className='menu-bars' onClick={showSidebar}/>
                </div>
                <div className='nav-text'>
                    <form className='login-form' onSubmit={handleSubmit}>
                        <label htmlFor='username' className='label'>Your Instagram Username</label>
                        <input className='login-input' ref={usernameRef} placeholder='your instagram username' />
                        <label htmlFor='password' className='label'>Your Instagram Password</label>
                        <input className='login-input' ref={passRef} type='password' placeholder='******' />
                        <label htmlFor='target' className='label'>Instagram Target Username</label>
                        <input className='login-input' ref={targetRef} placeholder='target instagram username' required />
                        <button className='login-button'>Go!</button>
                        <label className='label warning'>*use only target field <br/> to get same user, if<br/> you used this before*</label>
                        <label className='label warning'>*kento_sunny_0401 is <br/>available for sample<br/> target (only use target<br/>  field)*</label>
                    </form>

                </div>

            </div>
            </nav>
        </IconContext.Provider>
    </>
  )
}

export default Navbar