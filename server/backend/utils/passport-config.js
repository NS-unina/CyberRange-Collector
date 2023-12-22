import passport from 'passport';
import BearerStrategy from 'passport-http-bearer'

const registerStrategy = () => {
    passport.use(new BearerStrategy.Strategy((token, done) => {
  if (token === process.env.BEARER) {
    return done(null, true);
  } else {
    return done(null, false);
  }
}));
}

export {registerStrategy}
