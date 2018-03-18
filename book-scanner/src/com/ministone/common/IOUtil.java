package com.ministone.common;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;

public class IOUtil {
	
	public static String toString(InputStream is, String encoding) throws IOException {
		if(encoding==null||encoding.equals("")) return null;
		
		String result = null;
		ByteArrayOutputStream baos = null;
		try {
			byte b[] = new byte[512];
			if (is != null) {
				baos = new ByteArrayOutputStream(is.available());
				int i = -1;
				while ((i = is.read(b)) > -1) {
					baos.write(b, 0, i);
				}
				result = baos.toString(encoding);
			}

		} catch (IOException e) {
			throw e;
		} finally {
			try {
				if (is != null)
					is.close();
				if (baos != null)
					baos.close();
			} catch (IOException e) {

			}
		}

		return result;
	}
}
