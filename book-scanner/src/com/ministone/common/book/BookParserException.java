package com.ministone.common.book;

/**
 * User: gjkv86
 * Date: 9/7/11
 * Time: 1:28 PM
 */
public class BookParserException extends Exception{
    public BookParserException() {
        super();    //To change body of overridden methods use File | Settings | File Templates.
    }

    public BookParserException(String message) {
        super(message);    //To change body of overridden methods use File | Settings | File Templates.
    }

    public BookParserException(String message, Throwable cause) {
        super(message, cause);    //To change body of overridden methods use File | Settings | File Templates.
    }

    public BookParserException(Throwable cause) {
        super(cause);    //To change body of overridden methods use File | Settings | File Templates.
    }
}
