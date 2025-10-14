import React, { createContext, useContext, useState } from 'react';

const UserContext = createContext();

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};

export const UserProvider = ({ children }) => {
  const [userData, setUserData] = useState(null);
  const [username, setUsername] = useState('');

  const updateUser = (username, data) => {
    setUsername(username);
    setUserData(data);
  };

  const clearUser = () => {
    setUsername('');
    setUserData(null);
  };

  return (
    <UserContext.Provider value={{ userData, username, updateUser, clearUser }}>
      {children}
    </UserContext.Provider>
  );
};

